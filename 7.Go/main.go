package main

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
)

func run() {
	//fmt.Println("run")

	cmd :=exec.Command("/proc/self/ece", append([]string{"child"},os.Args[2:]...)...)

	//cmd := exec.Command(os.Args[2], os.Args[3:]...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr {
		//hostname에 대한 새로운 namespace를 만들어 주세요.
		Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID,
	}

	syscall.Sethostname([]byte("test"))
	syscall.Chroot("./MY_ROOT")
	syscall.Chdir("/")

	//syscall.Sethostname([]byte("test")) -> Hostname 변경 (vm 조심..)

	cmd.Run()

}

func child(){
	fmt.Printf("Running %v as pid %d\n", os.Args[2:], os.Getpid())
	cmd :=exec.Command("/proc/self/ece", append([]string{"child"},os.Args[2:]...)...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr {
		Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID,
	}

	cmd.Run()

}

// func exec() {
// 	fmt.Println("exec")
// }

// docker run <container-name>
// go run main.go run ls
func main() {
	fmt.Printf("Running %v as pid %d\n", os.Args[2:], os.Getpid())
	switch os.Args[1] {
	case "run":
		run()
	
	case "child":
		child()


//	case "exec":
//		exec()

	default:
		panic("help")
	}


}
