#! /bin/bash

# http://notes.restdesc.org/2011/images/index.html
export eulerjarpath="../../Euler.jar"


#java -jar $eulerjarpath --nope --pass agent_image.n3 description_images.n3
#java -jar $eulerjarpath --nope --pass server_image.n3 description_thumbnail.n3
#java -jar $eulerjarpath --help
#java -jar $eulerjarpath --nope --quick-answer agent_goal.n3 light_get.n3 light_post.n3
java -jar $eulerjarpath --nope --pass agent_goal.n3 light_get.n3 light_post.n3