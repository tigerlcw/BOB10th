#include <pcap.h>
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>
//라이브넷 라이브러리가 왜 인식을 못하지??
void usage() {
   printf("syntax: pcap-test <interface>\n");
    printf("sample: pcap-test eth0\n");
    printf("[bob10][개발]pcap-test[이찬우]");
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
        printf("TCP Destination : %x%x\n", packet[36],packet[37]);
        printf("TCP Source : %s%s\n", packet[34],packet[35]);
        printf("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ \n");
        printf("Payload Data 8Byte : %02x %02x %02x %02x %02x %02x %02x %02x\n",packet[54],packet[55],packet[56],packet[57],packet[58],packet[59],packet[60],packet[61]);
        printf("■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ \n");
        sleep(1);
   }

   pcap_close(pcap);
}
