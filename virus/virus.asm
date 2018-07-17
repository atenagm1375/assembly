section .text:
    global virus_start

virus_start:


virus_exit:
    xor     rax, rax
    inc     rax
    xor     rbx, rbx
    int     0x80
