FROM alpine:3.20

RUN apk add --no-cache dhcp
RUN touch /var/lib/dhcp/dhcpd.leases

EXPOSE 67/udp

ENTRYPOINT ["dhcpd", "-f", "-d", "--no-pid"]
