package main

import (
	"os"
	"fmt"
    "io/ioutil"
	"net/http"

	"github.com/gin-gonic/gin"
)

// https://raw.githubusercontent.com/gin-gonic/examples/master/basic/main.go
func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
        return value
    }
    return fallback
}

func getRequest(c *gin.Context) {
	nginx_host := getEnv("NGINX_HOST", "127.0.0.1")
	nginx_port := getEnv("NGINX_PORT", "8089")
	resp, err := http.Get(fmt.Sprintf("http://%s:%s/v1/hello", nginx_host, nginx_port))
	if err != nil {
		c.JSON(http.StatusOK, gin.H{"error": err, "code": 500})
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			c.JSON(http.StatusOK, gin.H{"error": err, "code": resp.StatusCode})
			return
		}
		bodyString := string(bodyBytes)
		c.JSON(http.StatusOK, gin.H{"data": bodyString, "code": resp.StatusCode})
		return
	} else {
		c.JSON(500, gin.H{"error": "500", "code": resp.StatusCode})
		return
	}
}

func setupRouter() *gin.Engine {
	// Disable Console Color
	// gin.DisableConsoleColor()
	r := gin.Default()

	r.GET("/v1/hello", func(c *gin.Context) {
		c.String(http.StatusOK, "hello")
	})
	r.GET("/v1/hello/get", getRequest)
	return r
}

func main() {
	r := setupRouter()
	// Listen and Server in 0.0.0.0:8080
	r.Run(":8095")
}