; exercise No.4, 08-Assembly.pdf
; write a program that sorts an array using bubble sort algorithm.
; run commands:
; nasm -f elf64 bubbleSort.asm
; ld -o ./bubbleSort -e _start ./bubbleSort.o
; gdb ./bubbleSort
; b test_while
; b exit
; r
; i r al
; c
; //repeat the above 2 until you have checked the whole array.
; q
section .data
    arr db 4, 2, 7, 8, 1, 6, 9, 3
    len equ $ - arr

section .bss
    sorted_array resb len

section .text
    global _start

_start:
    mov rsi, arr
    mov rdi, sorted_array
    mov rcx, len
    transfer_while:
        mov al, [rsi]
        mov [rdi], al
        inc rsi
        inc rdi
        loop transfer_while
    call bubble_sort

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

bubble_sort:
    mov cx, len
    for1:
        cmp cx, 0
        je end_for1
        mov rsi, sorted_array
        mov rdi, sorted_array
        inc rdi
        mov dx, 1
        for2:
            cmp dx, cx
            jge end_for2
            mov al, byte[rsi]
            cmp al, byte[rdi]
            jle continue
            mov bl, byte[rdi]
            mov [rdi], al
            mov [rsi], bl
            continue:
            inc dx
            inc rdi
            inc rsi
            jmp for2
        end_for2:
        dec cx
        jmp for1
    end_for1:
    ; test the result
    mov rsi, sorted_array
    mov cx, len
    test_while:
        mov al, byte[rsi]
        inc rsi
        loop test_while
    ret
