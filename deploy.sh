#!/usr/bin/env bash

create_service_account() {
    echo "${SERVICE_ACCOUNT}" | base64 -di > account.json
    echo "success!"
}

main(){
    create_service_account
}

main