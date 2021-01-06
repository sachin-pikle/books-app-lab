


book
```
{
    "isbn": "1",
    "title": "Java - The Complete Reference",
    "author": "Herbert Schildt"
}
```

listBooks



getBookByID

```
fn config app <app-name> BUCKET_NAME <wallet-bucket-name>
fn config app <app-name> COLLECTION_NAME <collection-name>
fn config app <app-name> DB_PASSWORD <db-password>
fn config app <app-name> DB_USER <db-user>
fn config app <app-name> NAMESPACE <namespace>
fn config app <app-name> TNS_NAME <tns-name>
```
```
fn config app books-app BUCKET_NAME wallet-bucket-name
fn config app books-app COLLECTION_NAME collection-name
fn config app books-app DB_PASSWORD db-password
fn config app books-app DB_USER db-user
fn config app books-app NAMESPACE namespace
fn config app books-app TNS_NAME tns-name
```


```
$(npm bin)/artillery quick \
    --count 5 \
    --num 1 \
    --output load-test/report.json \
    https://CHANGEME.apigateway.us-ashburn-1.oci.customer-oci.com/v1/books
```

```
$(npm bin)/artillery run load-test/get-all-books-view-details.yml
```


Node Js functions: how to access config variables? 
```
Let paramterValue = ctx.config.<paramatername>;
```
https://www.ateam-oracle.com/how-to-implement-an-oci-api-gateway-authorization-fn-in-nodejs-that-accesses-oci-resources


https://github.com/fnproject/fdk-node/blob/master/fn-fdk.js


https://github.com/fnproject/fdk-node/tree/master/examples
