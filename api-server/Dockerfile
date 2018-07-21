FROM golang:alpine as build-env

# Try hard to get a minimal image to reduce footprint
RUN apk update && \
    apk add go git gcc libc-dev libltdl libtool libgcc && \
    # Install go.rice
	go get github.com/GeertJohan/go.rice/rice && \
    # Install CFSSL
    git clone --depth=1 "https://github.com/cloudflare/cfssl.git" "${GOPATH}/src/github.com/cloudflare/cfssl" && \
    cd "${GOPATH}/src/github.com/cloudflare/cfssl" && \
    rice embed-go -i=./cli/serve && \
    go build -o /usr/bin/cfssl ./cmd/cfssl && \
	go build -o /usr/bin/cfssljson ./cmd/cfssljson && \
	go build -o /usr/bin/mkbundle ./cmd/mkbundle && \
	go build -o /usr/bin/multirootca ./cmd/multirootca && \
    apk del go git gcc libc-dev libtool libgcc


FROM alpine
COPY --from=build-env /usr/bin/cfssl /bin
VOLUME [ "/etc/cfssl" ]
EXPOSE 8888
ENTRYPOINT ["/bin/cfssl"]