package utils

import (
	"os"
	"path/filepath"
	"strings"
)

func FSOExpandUser(path string) (string, error) {
    if strings.HasPrefix(path, "~") {

    	  dirname, _ := os.UserHomeDir()
    		path = filepath.Join(dirname, path[2:])	
    }
    return path, nil
}