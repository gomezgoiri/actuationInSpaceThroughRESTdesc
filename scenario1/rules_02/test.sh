#! /bin/bash

# http://notes.restdesc.org/2011/images/index.html

#java -jar ../Euler.jar --nope --pass agent_image.n3 description_images.n3
#java -jar ../Euler.jar --nope --pass server_image.n3 description_thumbnail.n3
#java -jar ../../Euler.jar --help
#java -jar ../../Euler.jar --nope --quick-answer agent_goal.n3 light_get.n3 light_post.n3
java -jar ../../Euler.jar --nope --quick-answer light_together.n3 --query light_goal.n3