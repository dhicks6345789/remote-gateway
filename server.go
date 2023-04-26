package main
// A simple proxy server for Guacamole. See original proxy server code at:
// https://dev.to/b0r/implement-reverse-proxy-in-gogolang-2cp4



import (
    "io"
    "fmt"
    "log"
    "time"
    "net/url"
    "net/http"
)

func main() {
    fmt.Println("Starting proxy server...")
    
    // Define origin server URL
    originServerURL, err := url.Parse("http://127.0.0.1:8080")
    if err != nil {
        log.Fatal("invalid origin server URL")
    }

    reverseProxy := http.HandlerFunc(func(rw http.ResponseWriter, req *http.Request) {
        fmt.Printf("[reverse proxy server] received request at: %s\n", time.Now())

        // set req Host, URL and Request URI to forward a request to the origin server
        req.Host = originServerURL.Host
        req.URL.Host = originServerURL.Host
        req.URL.Scheme = originServerURL.Scheme
        req.RequestURI = ""

      // Save the response from the origin server.
        originServerResponse, err := http.DefaultClient.Do(req)
        if err != nil {
            rw.WriteHeader(http.StatusInternalServerError)
            _, _ = fmt.Fprint(rw, err)
            return
        }
        
        // Return response to the client.
        rw.WriteHeader(http.StatusOK)
        io.Copy(rw, originServerResponse.Body)
    })

    log.Fatal(http.ListenAndServe(":8090", reverseProxy))
}
