package main

// go is ; nono ok
import "fmt" // include<stdio.h>

func my_func() {
	fmt.Println("고랭 함수 사용법")
}

func main() { // int main(int argc, char **argv){ }

	var i int
	var j int = 2
	k := 3
	var str = "한글"
	var name string

	fmt.Print("hello, gogogo!! 이름 적으삼 :")
	fmt.Scan(&name)
	fmt.Println(name)
	fmt.Println("i=", i)
	fmt.Println("j=", j)
	fmt.Println("k=", k)
	fmt.Println("str=", str)

	for m := 1; m <= 5; m++ {
		fmt.Println("m=", m)
	}

	// var scores [3]int = [...]int{10,20,30}
	var scores [3]int = [...]int{10, 20, 30}
	for i := 0; i < len(scores); i++ {
		fmt.Println(scores[i])
	}
	my_func()
}

// gcc -o hello hello.c -> go run hello.go
