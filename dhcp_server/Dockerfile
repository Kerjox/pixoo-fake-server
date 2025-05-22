FROM alpine:3.20

RUN apk add --no-cache dhcp

EXPOSE 67/udp

ENTRYPOINT ["dhcpd", "-f", "-d", "--no-pid"]
