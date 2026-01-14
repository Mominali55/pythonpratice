#include <uapi/linux/bpf.h>
#include <uapi/linux/if_ether.h>
#include <uapi/linux/if_packet.h>
#include <uapi/linux/if_vlan.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/in.h>

// Define the hash map: key=u32 (IPv4 address), value=u64 (drop count)
BPF_HASH(blocklist, u32, u64);

// Cursor struct for parsing
struct cursor {
    void *pos;
    void *end;
};

// Helper to check packet boundaries
static __always_inline int parse_eth(struct cursor *c, struct ethhdr **eth) {
    struct ethhdr *eth_start = c->pos;
    if ((void *)(eth_start + 1) > c->end)
        return -1;
    *eth = eth_start;
    c->pos = (void *)(eth_start + 1);
    return 0;
}

static __always_inline int parse_ip(struct cursor *c, struct iphdr **ip) {
    struct iphdr *ip_start = c->pos;
    if ((void *)(ip_start + 1) > c->end)
        return -1;
    *ip = ip_start;
    c->pos = (void *)(ip_start + 1);
    return 0;
}

int xdp_filter(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    // Initialize cursor
    struct cursor c;
    c.pos = data;
    c.end = data_end;

    // 1. Verify packet boundaries & Parse Ethernet Header
    struct ethhdr *eth;
    if (parse_eth(&c, &eth) < 0) {
        return XDP_PASS;
    }

    // 2. Check if the protocol is IPv4
    if (eth->h_proto != htons(ETH_P_IP)) {
        return XDP_PASS;
    }

    // 3. Extract the Source IP
    struct iphdr *ip;
    if (parse_ip(&c, &ip) < 0) {
        return XDP_PASS;
    }
    
    u32 saddr = ip->saddr;

    // 4. Lookup the Source IP in the blocklist map
    u64 *drop_count = blocklist.lookup(&saddr);

    // 5. If found, increment the drop count and return XDP_DROP
    if (drop_count) {
        lock_xadd(drop_count, 1);
        return XDP_DROP;
    }

    // 6. If not found, return XDP_PASS
    return XDP_PASS;
}
