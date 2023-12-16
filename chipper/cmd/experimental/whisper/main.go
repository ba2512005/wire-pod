package main

import (
	"fmt"
	"log"
	"os/exec"

	"./initwirepod"
	stt "./whisper"
)

func main() {
	initwirepod.StartFromProgramInit(stt.Init, stt.STT, stt.Name)

	// Command to run the Python script with arguments if needed
	cmd := exec.Command("python3", "wire-pod/Whisper_local.py")

	// Run the command and handle any errors
	output, err := cmd.CombinedOutput()
	if err != nil {
		log.Fatalf("Error running Python script: %v\n", err)
	}

	// Print the output of the Python script
	fmt.Printf("Output:\n%s\n", output)
}

fun fib() {
}