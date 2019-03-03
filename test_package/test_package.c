#include <rpc/xdr.h>

int main()
{
    XDR xdr;
    xdrrec_create(&xdr, 65536, 0, 0, 0, 0);
    return 0;
}
