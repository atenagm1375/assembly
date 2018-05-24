; Project No.1
; a calculator with the 4 simple operations
; each line contains two numbers seperated with an operator
; the result of each line will be printed on the line below it as the first operand of the other operation
; each line ends with an =
; example input: 5+3=
section .data
    msg db "Enter valid operation or x to exit:", 10
    msg_len equ $-msg
    error db "Illegal operation. Please, try again.", 10
    error_len equ $-error
    divide_by_zero db "divide by zero. go to start?(y or n)", 10
    div_len equ $-divide_by_zero
    result dq 0
    max_num_size equ 19                 ; max digits of an integer
    max_inp_size equ 40                 ; max size of input string

section .bss
    inp resb max_inp_size               ; keeps the input
    num resb max_num_size              ; keeps a number
    op resb 1                           ; keeps operator
    flag resb 1                         ; flags

section .text
    global _start

_start:
    mov rax, 1
    mov rdi, 0
    mov rsi, msg                        ; start message
    mov rdx, msg_len
    syscall
    mov al, 1
    mov [flag], al

    start_while:
    call readUserInput
    cmp [rsi], byte 'x'
    je exit
    call evaluateInput                  ; analyze input
    call error_occured
    call doOperation                    ; do the corresponding operation
    call itoa                           ; change the resulting integer into characters so that it is printable
    call printResult                    ; print the result
    call clear_num                      ; clear num array for further instructions
    xor rax, rax
    mov [flag], al
    jmp start_while

exit:
    mov rax, 1
    mov rbx, 0
    int 80h

error_occured:
    mov bl, 8
    and bl, [flag]
    cmp bl, 8
    je _start
    ret

readUserInput:
    mov rcx, max_inp_size
    mov rsi, inp
    xor bl, bl
    clear_while:                        ; clear input buffer before reading a new input
        mov [rsi], bl
        inc rsi
        loop clear_while
    ; sys_read: %rax: 0, %rdi: unsigned int fd, %rsi: char *buf, %rdx: size_t count
    mov rax, 0
    mov rdi, 0
    mov rsi, inp
    mov rdx, max_inp_size
    syscall
    ret

printResult:
    ; sys_write: %rax: 1, %rdi: unsigned int fd, %rsi: char *buf, %rdx: size_t count
    mov rax, 1
    mov rdi, 0
    mov rsi, num
    mov rdx, max_num_size
    syscall
    ret

printError:
    mov rax, 1
    mov rdi, 0
    mov rsi, error
    mov rdx, error_len
    syscall
    mov bl, 8
    sub [flag], bl
    ret

evaluateInput:
    mov rsi, inp
    mov rdi, num
    mov rcx, max_inp_size
    mov al, [flag]
    cmp al, 0
    je not_a_number
    mov bl, 2
    mov r12b, byte '-'
    cmp r12b, [rsi]
    jne evaluate_while
    add [flag], bl
    inc rsi
    evaluate_while:
        mov bl, 1
        and bl, [flag]
        cmp bl, 1
        je go
        mov r8, [result]
        go:
        mov r12b, byte[rsi]

        cmp r12b, byte '0'
        jl not_a_number
        cmp r12b, byte '9'
        jg not_a_number

        mov al, r12b                       ; put first number characters in num array(if first number exists)
        mov [rdi], al
        inc rdi
        inc rsi
        jmp evaluate_while

    not_a_number:
    mov r12b, [rsi]
    cmp r12b, byte '='                  ; find = as it is the end of input
    je end_evalute_while

    cmp r12b, byte '+'                  ; find the operator
    je continue_eval

    cmp r12b, byte '-'
    je continue_eval

    cmp r12b, byte '*'
    je continue_eval

    cmp r12b, byte '/'
    je continue_eval

    call printError
    mov r11b, 8
    add [flag], r11b
    ret

    continue_eval:
    mov [op], r12b
    inc rsi
    mov bl, 1
    and bl, [flag]
    cmp bl, 1
    jne no_first_operand
    call atoi
    mov r8, r9
    no_first_operand:
    mov r12b, 2
    mov bl, byte '-'
    cmp bl, [rsi]
    jne not_negative
    add [flag], r12b
    inc rsi
    not_negative:
    mov r9, [result]
    jmp evaluate_while
    end_evalute_while:
    call atoi
    ret

clear_num:
    mov cx, max_num_size
    mov rdi, num
    xor bl, bl
    clear_num_while:
        mov [rdi], bl
        inc rdi
        dec cx
        cmp cx, 0
        jne clear_num_while
    mov rdi, num
    ret

atoi:
    mov rdi, num
    xor r9, r9
    xor rax, rax
    xor rdx, rdx
    mov r10, 10
    cmp byte[rdi], al
    ; je end_atoi_error

    atoi_while:
        mul r10
        mov bl, [rdi]
        sub bl, byte '0'
        add rax, rbx
        inc rdi
        cmp byte[rdi], byte 0
        jne atoi_while

    mov bl, 2
    and bl, [flag]
    cmp bl, 2
    jne positive
    neg rax
    sub [flag], bl
    positive:
    mov r9, rax
    call clear_num
    end_atoi:
    ret
    end_atoi_error:
    call printError
    mov r11b, 8
    add [flag], r11b
    ret

itoa:
    mov rax, [result]
    mov rdi, num
    mov r10, 10
    mov r11b, byte '-'
    jns itoa_while
    neg rax
    mov [rdi], r11b
    inc rdi
    itoa_while:
        xor rdx, rdx
        div r10
        add dl, byte '0'
        mov [rdi], dl
        inc rdi
        cmp rax, 0
        jne itoa_while
    dec rdi
    mov rsi, num
    cmp byte[rsi], r11b
    jne mirror_while
    inc rsi
    mirror_while:
        cmp rsi, rdi
        jge end_mirror_while
        mov bl, byte[rsi]
        mov dl, byte[rdi]
        mov [rsi], dl
        mov [rdi], bl
        inc rsi
        dec rdi
        jmp mirror_while
    end_mirror_while:
    ret

doOperation:
    xor rbx, rbx
    mov bl, [op]
    mov [result], r8
    cmp bl, byte '+'
    je add_op
    cmp bl, byte '-'
    je sub_op
    cmp bl, byte '*'
    je mul_op
    cmp bl, byte '/'
    je div_op

    add_op:
    add [result], r9
    jmp end_doOperation

    sub_op:
    sub [result], r9
    jmp end_doOperation

    mul_op:
    mov rax, [result]
    imul r9
    mov [result], rax
    jmp end_doOperation

    div_op:
    cmp r9, 0
    je divided_by_zero
    mov rax, [result]
    cqo
    idiv r9
    neg rax
    neg rax
    mov [result], rax
    jmp end_doOperation

    divided_by_zero:
    mov rax, 1
    mov rdi, 0
    mov rsi, divide_by_zero
    mov rdx, div_len
    syscall
    ; mov rax, [result]
    ; neg rax
    ; neg rax
    jmp _start

    end_doOperation:
    ret

    end_doOperation_error:
    mov r11b, 8
    add [flag], r11b
    ret
