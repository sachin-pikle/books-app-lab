ETL permissions:

allow dynamic-group dg-compartment-sachin-pikle to manage objects in compartment sachin-pikle where any { target.bucket.name='books-ETL-input' , target.bucket.name='books-ETL-processed' }


fn config function gh-app books-etl-python ordsbaseurl "https://CHANGEME.adb.us-ashburn-1.oraclecloudapps.com/ords/"

fn config function gh-app books-etl-python dbpwd <dbpwd>