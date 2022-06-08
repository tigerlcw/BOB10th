#include <pcap.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <libnet.h>
#include <string.h> // memcpy

struct libnet_tcp_hdr tcp_hdr; // lib TCP

void usage() {
   printf("syntax: pcap-test <interface>\n");
   printf("sample: pcap-test eth0\n");
   printf("[bob10][개발]pcap-test[이찬우]\n");
}

typedef struct {
   char* dev_;
} Param;

Param param  = {
   .dev_ = NULL
};

bool parse(Param* param, int argc, char* argv[]) {
   if (argc != 2) {
      usage();
      return false;
   }
   param->dev_ = argv[1];
   return true;
}

void tcp_out(const u_char* packet) {
    memcpy(&tcp_hdr, &packet[34], sizeof (tcp_hdr)); //34 tcp data
    printf("TCP Source Port: %d\n",ntohs(tcp_hdr.th_sport));
    printf("TCP Destination port: %d\n",ntohs(tcp_hdr.th_dport));
    return;
}

int main(int argc, char* argv[]) {
   if (!parse(&param, argc, argv))
      return -1;

   char errbuf[PCAP_ERRBUF_SIZE];
   pcap_t* pcap = pcap_open_live(param.dev_, BUFSIZ, 1, 1000, errbuf);
   if (pcap == NULL) {
      fprintf(stderr, "pcap_open_live(%s) return null - %s\n", param.dev_, errbuf);
      return -1;
   }

   while (true) {
      struct pcap_pkthdr* header;
      const u_char* packet;
      int res = pcap_next_ex(pcap, &header, &packet);
      if (res == 0) continue;
      if (res == PCAP_ERROR || res == PCAP_ERROR_BREAK) {
         printf("pcap_next_ex return %d(%s)\n", res, pcap_geterr(pcap));
         break;
      }

        // out data
        printf("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ \n");
        printf("Ethernet Destination : %02x:%02x:%02x:%02x:%02x:%02x\n", packet[0],packet[1],packet[2],packet[3],packet[4],packet[5]);
        printf("Ethernet Source : %02x:%02x:%02x:%02x:%02x:%02x\n", packet[6],packet[7],packet[8],packet[9],packet[10],packet[11]);
        printf("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ \n");
        printf("IPv4 Destination : %d.%d.%d.%d\n", packet[30],packet[31],packet[32],packet[33]);
        printf("IPv4 Source : %u.%u.%u.%u\n", packet[26],packet[27],packet[28],packet[29]);
        printf("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ \n");
        tcp_out(packet);
        printf("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ \n");
        printf("Payload Data 8Byte : %02x %02x %02x %02x %02x %02x %02x %02x\n",packet[54],packet[55],packet[56],packet[57],packet[58],packet[59],packet[60],packet[61]);
        printf("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ \n");
   }

   pcap_close(pcap);
}
