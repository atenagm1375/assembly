global _start
_start:     push    byte 4
            pop     rax
            xor     rbx, rbx
            inc     rbx
            mov     rcx, 0x0000000000400001
            push    byte 3
            pop     rdx
            int     0x80

            xor     rax, rax
            inc     rax
            xor     rbx, rbx
            int     0x80
