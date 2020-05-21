FROM golang:latest

RUN  mkdir -p /go/src \
  && mkdir -p /go/bin \
  && mkdir -p /go/pkg
ENV GOPATH=/go
ENV PATH=$GOPATH/bin:$PATH   

WORKDIR $GOPATH/src/github.com/seekplum/gin-stress

ADD . $GOPATH/src/github.com/seekplum/gin-stress
RUN go build -o main .

EXPOSE 8095
CMD ["./main"]