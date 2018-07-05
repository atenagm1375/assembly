; Ashena G.Mohammadi, 610394128
; calculator with the simple arithmetic functions-summation, multiplication,
; division, and subtraction-for both integers and floating point numbers

;******************************************************************************
;******************************************************************************

%macro hiprec 2
    push rax
    mov al, %1
    cmp al, byte '/'
    je check_second
    cmp al, byte '*'
    je check_second
    jmp end_hiprec

    check_second:
    mov al, %2
    cmp al, byte '+'
    je is_higher
    cmp al, byte '-'
    je is_higher
    jmp end_hiprec

    is_higher:
    mov ax, higherprec
    bts [calc_flag], ax

    end_hiprec:
    pop rax
%endmacro

section .data
    msg db "Enter a valid operation or q to exit:", 10
    msg_len equ $-msg
    errormsg db "Illegal operation. Please, try again.", 10
    error_len equ $-errormsg
    divide_by_zero db "divide by zero", 10
    div_len equ $-divide_by_zero

    termios times 36 db 0
    stdin equ 0
    ICANON equ 1<<1
    ECHO equ 1<<3
    sys_read equ 3
    sys_write equ 4
    stdout equ 1

    isfloat equ 1
    opentered equ 2
    numentered equ 3
    erroccured equ 4
    higherprec equ 5
    isneg equ 6

    max_size equ 15
    calc_flag db 0
    num_len db 0
    dot_pos db 0
    num dq 0
    ten dq 10

;******************************************************************************

section .bss
    op_stack resb max_size      ; operators' stack
    num_stack resq max_size     ; operands' stack
    inp resb 1                  ; holds input char

;******************************************************************************

section .text
    global _start

_start:
    call canonical_off
    call evaluate_expression

;------------------------------------------------------------------------------

exit:
    call canonical_on
    mov rax, 1
    mov rbx, 0
    int 80h

;------------------------------------------------------------------------------

evaluate_expression:
    mov rsi, num_stack
    mov rdi, op_stack
    mov r10, 10
    read_loop:
        call read_char
        call evaluate_char
        mov bx, erroccured
        bt [calc_flag], bx
        jnc read_loop
    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    xor rdx, rdx
    mov qword[num], 0
    mov byte[calc_flag], 0
    mov byte[num_len], 0
    mov byte[dot_pos], 0
    jmp evaluate_expression

;..............................................................................

read_char:
    ; save contents of registers
    push rax
    push rbx
    push rcx
    push rdx

    ; sys_read
    mov byte [inp], 0
    mov rax, sys_read
    mov rbx, stdin
    mov rcx, inp
    mov edx, 2
    int 80h

    ; retrieve contents of registers
    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret

;..............................................................................

evaluate_char:
    ; save contents of registers
    push rax
    push rbx

    ; check quit command
    mov al, byte 'q'
    cmp al, [inp]
    je exit

    ;check end of line
    mov al, byte '='
    cmp al, [inp]
    jne dot
    call push_number
    call calculate
    call print_result
    jmp end_evaluate_char

    ; check for .
    dot:
    mov al, byte '.'
    cmp al, [inp]
    jne plus
    mov al, [num_len]
    mov [dot_pos], al
    mov ax, isfloat
    bts [calc_flag], ax
    jmp end_evaluate_char

    ; check operators
    plus:
    mov al, byte '+'
    cmp al, [inp]
    jne minus
    call push_number
    call evaluate_operator
    jmp end_evaluate_char

    minus:
    mov al, byte '-'
    cmp al, [inp]
    jne star
    call push_number
    call evaluate_operator
    jmp end_evaluate_char

    star:
    mov al, byte '*'
    cmp al, [inp]
    jne divide
    call push_number
    call evaluate_operator
    jmp end_evaluate_char

    divide:
    mov al, byte '/'
    cmp al, [inp]
    jne digit
    call push_number
    push qword[inp]
    call evaluate_operator
    jmp end_evaluate_char

    ; check digit
    digit:
    mov al, byte '9'
    cmp al, [inp]
    jl char_error
    mov al, byte '0'
    cmp al, [inp]
    jg char_error
    xor rbx, rbx
    mov bl, [inp]
    sub bl, al
    push rbx
    call atoi
    mov ax, numentered
    bts [calc_flag], ax
    mov ax, opentered
    btr [calc_flag], ax
    jmp end_evaluate_char

    ; invalid expression
    char_error:
    call invalid_exp_err

    end_evaluate_char:
    ; retrieve contents of registers
    pop rbx
    pop rax
    ret

;..............................................................................

push_number:
    ; save registers' contents
    push rax
    push rbx
    push rcx

    mov bx, numentered
    btr [calc_flag], bx

    mov bx, isneg
    bt [calc_flag], bx
    jnc continue
    neg qword[num]

    continue:
    mov bx, isfloat
    bt [calc_flag], bx
    jc push_float
    mov rax, [num]
    mov [rsi], rax
    jmp end_pushing

    push_float:
    xor rcx, rcx
    mov cl, [num_len]
    sub cl, [dot_pos]
    fild qword[ten]
    fld qword[num]
    convert_to_float_loop:
        fdiv st1
        loop convert_to_float_loop
    fst qword[rsi]

    end_pushing:
    add rsi, 8
    mov qword[num], 0
    mov byte[dot_pos], 0
    mov byte[num_len], 0
    ; retrieve registers' contents
    pop rcx
    pop rbx
    pop rax
    ret

;..............................................................................

evaluate_operator:
    enter 8, 0
    ; save registers' contents
    mov [rbp - 8], rax

    mov ax, opentered
    bt [calc_flag], ax
    jnc check_prec
    mov al, '-'
    cmp [rbp + 16], al
    jne operator_error
    cmp [rdi], al
    jne operator_error
    mov ax, isneg
    btc [calc_flag], ax
    jmp end_evaluate_operator

    check_prec:
    hiprec byte[rbp + 16], byte[rdi]
    jc push_operator

    push_operator:
    mov al, [rbp + 16]
    mov [rdi], al
    inc rdi
    jmp end_evaluate_operator

    operator_error:
    call invalid_exp_err

    end_evaluate_operator:
    mov ax, opentered
    bts [calc_flag], ax
    ; retrieve registers' contents
    mov rax, [rbp - 8]

    leave
    ret 8

;..............................................................................

atoi:
    enter 16, 0
    ; save registers' contents
    mov [rbp - 8], rax
    mov [rbp - 16], rdx

    mov rax, [num]
    mul r10
    add rax, [rbp + 16]
    mov [num], rax
    inc byte [num_len]

    ; retrieve contents of registers
    mov rdx, [rbp - 16]
    mov rax, [rbp - 8]
    leave
    ret 8

;..............................................................................

calculate:
    ret

;..............................................................................

print_result:
    ret

;..............................................................................

invalid_exp_err:
    ; save registers' contents
    push rax
    push rbx
    push rcx
    push rdx

    mov rax, sys_write
    mov rbx, stdout
    mov rcx, errormsg
    mov rdx, error_len
    int 80h

    mov bx, erroccured
    bts [calc_flag], bx

    ; retrieve registers' contents
    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret

;------------------------------------------------------------------------------

canonical_off:
    call read_stdin_termios

    ; clear canonical bit in local mode flags
    push rax
    mov eax, ICANON
    not eax
    and [termios+12], eax
    pop rax

    call write_stdin_termios
    ret

;..............................................................................

echo_off:
    call read_stdin_termios

    ; clear echo bit in local mode flags
    push rax
    mov eax, ECHO
    not eax
    and [termios+12], eax
    pop rax

    call write_stdin_termios
    ret

;..............................................................................

canonical_on:
    call read_stdin_termios

    ; set canonical bit in local mode flags
    or dword [termios+12], ICANON

    call write_stdin_termios
    ret

;..............................................................................

echo_on:
    call read_stdin_termios

    ; set echo bit in local mode flags
    or dword [termios+12], ECHO

    call write_stdin_termios
    ret

;..............................................................................

read_stdin_termios:
    push rax
    push rbx
    push rcx
    push rdx

    mov eax, 36h
    mov ebx, stdin
    mov ecx, 5401h
    mov edx, termios
    int 80h

    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret

;..............................................................................

write_stdin_termios:
    push rax
    push rbx
    push rcx
    push rdx

    mov eax, 36h
    mov ebx, stdin
    mov ecx, 5402h
    mov edx, termios
    int 80h

    pop rdx
    pop rcx
    pop rbx
    pop rax
    ret
