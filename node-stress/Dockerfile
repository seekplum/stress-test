FROM node:12
ADD . /data/npm
WORKDIR /data/npm
RUN npm install --registry=http://r.cnpmjs.org
CMD ["/bin/bash", "-c", "env && node main.js"]
