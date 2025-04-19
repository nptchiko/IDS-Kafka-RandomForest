# #!/bin/bash
# if [ "$MONGO_INITDB_ROOT_USERNAME" ] && [ "$MONGO_INITDB_ROOT_PASSWORD" ]; then
#   mongosh "admin" --quiet <<-EOJS
#     db.createUser({
#       user: "$MONGO_INITDB_ROOT_USERNAME",
#       pwd: "$MONGO_INITDB_ROOT_PASSWORD",
#       roles: [ "root" ]
#     })
# EOJS
# fi
# echo "======================================================"
# echo "created $MONGO_INITDB_ROOT_USERNAME in database admin"
# echo "======================================================"
