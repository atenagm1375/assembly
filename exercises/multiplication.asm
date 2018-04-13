; exercise No.3, 10-assembly4.pdf
; write a program that does the multiplication using addition{al*bl=ah:al}
section .text
    global _start

_start:
    mov al, 20
    mov bl, 19
    call multiplication

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

multiplication:
    xor cx, cx
    cmp al, 0
    cmove ax, cx
    jmp end
    cmp bl, 0
    cmove ax, cx
    jmp end
    mov cl, bl
    movzx dx, al
    dec cl
    while:
        add ax, dx
        loop while
    end:
    ret
