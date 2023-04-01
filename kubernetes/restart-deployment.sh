#!/bin/bash

kubectl delete deployment $1
kubectl delete service $2

kubectl apply -f $3
kubectl apply -f $4
