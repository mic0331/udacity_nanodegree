For information,

The OSM and JSON file has been removed from the repository.
The following git command has been used :

````shell
# Stage our giant file for removal, but leave it on disk
git rm --cached data/brussels_belgium.osm
git rm --cached data/brussels_belgium.osm.json

# Amend the previous commit with your change
# Simply making a new commit won't work, as you need
# to remove the file from the unpushed history as well
git commit --amend -CHEAD

# Push our rewritten, smaller commit
git push
````