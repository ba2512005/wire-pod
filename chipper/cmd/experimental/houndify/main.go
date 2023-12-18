package main

import (
	"github.com/ba2512005/wire-pod/chipper/pkg/initwirepod"
	stt "github.com/ba2512005/wire-pod/chipper/pkg/wirepod/stt/houndify"
)

func main() {
	initwirepod.StartFromProgramInit(stt.Init, stt.STT, stt.Name)
}
