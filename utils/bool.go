package utils

import (
  "strconv"
)

func AllTrue(b ...any) bool {

	if len(b) == 0 {
		return false
	} else if len(b) == 1 {
	  switch v := b[0].(type) {
	  	case string:
	  	  bs0, err := strconv.ParseBool(b[0].(string))
	  	  if err != nil {
	  	  	return len(b[0].(string)) > 0 
	  	  } else {
	  	  	return bs0
	  	  }
	  	case int:
	  		return b[0].(int) > 0
	  	default:
	  	  return v.(bool)
	  }	
	}

  switch v := b[0].(type) {
    case string:
      bs0, err := strconv.ParseBool(b[0].(string))
      if err != nil {
      	return len(b[0].(string)) > 0 && AllTrue(b[1:]...)
      } else {
      	return bs0 && AllTrue(b[1:]...)
      }
    case int:
      return b[0].(int) > 0 && AllTrue(b[1:]...)
    default:
      return v.(bool) && AllTrue(b[1:]...)
  }		
	
}