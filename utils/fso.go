package utils

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"syscall"
)

func FSOExpandUser(path string) (string, error) {
    if strings.HasPrefix(path, "~") {

    	  dirname, _ := os.UserHomeDir()
    		path = filepath.Join(dirname, path[2:])	
    }
    return path, nil
}

func FSOGlob(root string, fn func(string)bool) []string {
   var files []string
   filepath.WalkDir(root, func(s string, d fs.DirEntry, e error) error {
      if fn(s) {
         files = append(files, s)
      }
      return nil
   })
   return files
}

func GetAllMatches(r *regexp.Regexp, f *os.File) ([]string, error) {
	
	var matches []string
	
	stat, err := f.Stat()
	if err != nil {
		return matches, err
	}
	d, err := syscall.Mmap(int(f.Fd()), 0, int(stat.Size()), syscall.PROT_READ, syscall.MAP_SHARED)
	if err != nil {
		return matches, err
	}
	defer syscall.Munmap(d)
	i := 0
	for {
		loc := r.FindIndex(d[i:])
		if loc == nil {
			break
		}
		matches = append(matches, fmt.Sprintf("%q\n", d[i+loc[0]:i+loc[1]]))
		i += loc[1]
	}
	return matches, err
}