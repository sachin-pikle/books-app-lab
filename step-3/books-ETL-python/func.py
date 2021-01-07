#
# oci-load-file-into-adw-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import oci
import logging
import requests

from fdk import response

# soda_insert uses the Autonomous Database REST API to insert JSON documents
def soda_insert(ordsbaseurl, dbschema, dbuser, dbpwd, collection, logentries):
    auth=(dbuser, dbpwd)
    sodaurl = ordsbaseurl + dbschema + '/soda/latest/'
    bulkinserturl = sodaurl + 'custom-actions/insert/' + collection + "/"
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(bulkinserturl, auth=auth, headers=headers, data=json.dumps(logentries))
    print("INFO - DB insert response:: ", resp.json(), flush=True)
    return resp.json()


def load_data(signer, namespace, bucket_name, object_name, ordsbaseurl, schema, dbuser, dbpwd, collection):
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    try:
        print("INFO - About to read object {0} in bucket {1}...".format(object_name, bucket_name), flush=True)
        # we assume the file can fit in memory, otherwise we have to use the "range" argument and loop through the file
        jsondata = client.get_object(namespace, bucket_name, object_name)
        if jsondata.status == 200:
            print("INFO - Object {0} is read".format(object_name), flush=True)
            input_json = str(jsondata.data.text)
            print("INFO - inserting: ", input_json, flush=True)
            #     print("INFO - " + json.dumps(row), flush=True)
            insert_status = soda_insert(ordsbaseurl, schema, dbuser, dbpwd, collection, input_json)
            # if "id" in insert_status["items"][0]:
            #     print("INFO - Successfully inserted document ID " + insert_status["items"][0]["id"], flush=True)
            # else:
            #     raise SystemExit("Error while inserting: " + insert_status)
        else:
            raise SystemExit("cannot retrieve the object" + str(object_name))
    except Exception as e:
        raise SystemExit(str(e))
    print("INFO - All documents are successfully loaded into the database", flush=True)


def move_object(signer, namespace, source_bucket, destination_bucket, object_name):
    objstore = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    objstore_composite_ops = oci.object_storage.ObjectStorageClientCompositeOperations(objstore)
    resp = objstore_composite_ops.copy_object_and_wait_for_state(
        namespace, 
        source_bucket, 
        oci.object_storage.models.CopyObjectDetails(
            destination_bucket=destination_bucket, 
            destination_namespace=namespace,
            destination_object_name=object_name,
            destination_region=signer.region,
            source_object_name=object_name
            ),
        wait_for_states=[
            oci.object_storage.models.WorkRequest.STATUS_COMPLETED,
            oci.object_storage.models.WorkRequest.STATUS_FAILED])
    if resp.data.status != "COMPLETED":
        raise Exception("cannot copy object {0} to bucket {1}".format(object_name,destination_bucket))
    else:
        resp = objstore.delete_object(namespace, source_bucket, object_name)
        print("INFO - Object {0} moved to Bucket {1}".format(object_name,destination_bucket), flush=True)


def handler(ctx, data: io.BytesIO=None):
    logger = logging.getLogger()
    logger.info("function start")
    signer = oci.auth.signers.get_resource_principals_signer()
    object_name = bucket_name = namespace = ordsbaseurl = schema = dbuser = dbpwd = ""
    try:
        cfg = ctx.Config()
        input_bucket = cfg["input-bucket"]
        processed_bucket = cfg["processed-bucket"]
        ordsbaseurl = cfg["ordsbaseurl"]
        schema = cfg["dbschema"]
        dbuser = cfg["dbuser"]
        dbpwd = cfg["dbpwd"]
        collection = cfg["collection"]
    except Exception as e:
        logger.error('Missing configuration keys: input-bucket, processed-bucket, ordsbaseurl, dbschema, dbuser, dbpwd and collection')
        raise

    try:
        body = json.loads(data.getvalue())
        print("INFO - Event ID {} received".format(body["eventID"]), flush=True)
        print("INFO - Object name: " + body["data"]["resourceName"], flush=True)
        object_name = body["data"]["resourceName"]
        print("INFO - Bucket name: " + body["data"]["additionalDetails"]["bucketName"], flush=True)
        if body["data"]["additionalDetails"]["bucketName"] != input_bucket:
            raise ValueError("Event Bucket name error")
        print("INFO - Namespace: " + body["data"]["additionalDetails"]["namespace"], flush=True)
        namespace = body["data"]["additionalDetails"]["namespace"]
    except Exception as e:
        print('ERROR: bad Event!', flush=True)
        raise
    load_data(signer, namespace, input_bucket, object_name, ordsbaseurl, schema, dbuser, dbpwd, collection)
    move_object(signer, namespace, input_bucket, processed_bucket, object_name)

    return response.Response(
        ctx, 
        response_data=json.dumps({"status": "Success"}),
        headers={"Content-Type": "application/json"}
    )
