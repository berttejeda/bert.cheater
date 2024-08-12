package utils

import (
  "reflect"
)

func HasAttr(obj interface{}, fieldName string) bool {
    v := reflect.ValueOf(obj)
    if v.Kind() != reflect.Struct {
        return false
    }

    field := v.FieldByName(fieldName)
    return field.IsValid()
}