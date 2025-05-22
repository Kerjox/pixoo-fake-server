FROM alpine:latest

RUN apk add --no-cache dhcp

EXPOSE 67/udp

ENTRYPOINT ["dhcpd", "-f", "-d", "--no-pid"]