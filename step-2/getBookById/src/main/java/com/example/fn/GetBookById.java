package com.example.fn;

import java.util.Arrays;
//import java.util.Map;

import com.fnproject.fn.api.FnConfiguration;
import com.fnproject.fn.api.OutputEvent;
import com.fnproject.fn.api.RuntimeContext;
import com.fnproject.fn.api.httpgateway.HTTPGatewayContext;

public class GetBookById {

    private String APP_NAME;
    private String FN_NAME;
    private BooksDatabaseImpl booksDB;

    // private Map<String,String> books = Map.of(
    //     "1", "{ \"isbn\": \"1\", \"title\": \"Java - The Complete Reference\", \"author\": \"Herbert Schildt\" }", 
    //     "2", "{ \"isbn\": \"2\", \"title\": \"Effective Java\", \"author\": \"Joshua Bloch\" }", 
    //     "3", "{ \"isbn\": \"3\", \"title\": \"Learning Python\", \"author\": \"Mark Lutz\" }", 
    //     "4", "{ \"isbn\": \"4\", \"title\": \"JavaScript: The Definitive Guide\", \"author\": \"David Flanagan\" }", 
    //     "5", "{ \"isbn\": \"5\", \"title\": \"Oracle SOA Suite 12c Handbook\", \"author\": \"Lucas Jellema\" }"
    // );

    @FnConfiguration
    public void setUp(RuntimeContext ctx) {
        APP_NAME = ctx.getConfigurationByKey("APP_NAME").orElse("NO-APP_NAME");
        FN_NAME = ctx.getConfigurationByKey("FN_NAME").orElse("NO-FN_NAME");
        booksDB = new BooksDatabaseImpl();
    }    
    
    public OutputEvent handleRequest(HTTPGatewayContext hctx, RuntimeContext ctx) {
        System.out.printf("Inside App Name: %s | Function Name: %s | Language: Java \n", APP_NAME, FN_NAME); 
        
        String requestURL = hctx.getRequestURL();
        System.out.printf("Request URL is: %s\n", requestURL);
        System.out.printf("Request URL is blank: %s\n", requestURL.isBlank());
        System.out.printf("Request URL is empty: %s\n", requestURL.isEmpty());

        String book = null;

        if (requestURL.isEmpty()) {
            System.out.printf("Request URL is empty: %s\n", requestURL.isEmpty());
            booksDB.getAll();

        } else {
            String[] strArray = requestURL.split("/");
            System.out.printf("strArray: %s\n", Arrays.toString(strArray));
            // The format is /v1/books/{bookId} so the bookId is at index 3 in the array
            String bookId = strArray[3];
            System.out.printf("BookId: %s\n", bookId); 
            
            // book = books.get(bookId);
            book = booksDB.getById(bookId);
            System.out.printf("Get Book: %s\n", book);     
        }
    

        OutputEvent out = null;

        if (book != null) {
            out = OutputEvent.fromBytes(
                book.getBytes(), // Data
                OutputEvent.Status.Success,     // Status code of 200
                "application/json"       // Content type
            );
        } else {
            book = "Book not found - Invalid Book Id";
            hctx.setStatusCode(404);
            out = OutputEvent.fromBytes(
                book.getBytes(), // Data
                OutputEvent.Status.Success,     // Status code of 200
                "text/plain"       // Content type
            );
        }

        return out;
    }

}