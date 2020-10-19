$image="apacheignite/ignite"
$node1="ignite-node-1"
$node2="ignite-node-2"

docker pull $image
docker stop $node1
docker rm $node1
docker stop $node2
docker rm $node2

$CONFIG_URI="https://raw.githubusercontent.com/rma7036/woo/main/cluster-config.xml"
$JVM_OPTS="-Xms1g -Xmx1g -server -XX:+AggressiveOpts -XX:MaxPermSize=256m"
docker run --ip 172.17.10.1 -d --name $node1 -e "JVM_OPTS=$JVM_OPTS" -e "CONFIG_URI=$CONFIG_URI" $image
docker run --ip 172.17.10.2 -d --name $node2 -e "JVM_OPTS=$JVM_OPTS" -e "CONFIG_URI=$CONFIG_URI" $image
