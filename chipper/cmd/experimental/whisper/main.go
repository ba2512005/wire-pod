package main

import (
    "fmt"
	"log"
	"os/exec"
	"wire-pod/chipper/pkg/initwirepod"
	stt "chipper/pkg/wirepod/stt/whisper/Whisper.go"
	"github.com/kercre123/wire-pod/chipper/pkg/initwirepod"
	stt "github.com/kercre123/wire-pod/chipper/pkg/wirepod/stt/whisper"
)

func main() {
	initwirepod.StartFromProgramInit(stt.Init, stt.STT, stt.Name)

	// Command to run the Python script with arguments if needed
	cmd := exec.Command("python", "wire-pod/chipper/pkg/wirepod/stt/whisper/Whisper_local.py")

	// Run the command and handle any errors
	output, err := cmd.CombinedOutput()
	if err != nil {
		log.Fatalf("Error running Python script: %s\n", err)
	}

	// Print the output of the Python script
	fmt.Printf("Output:\n%s\n", output)
}
