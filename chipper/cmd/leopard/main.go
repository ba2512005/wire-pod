package main

import (
	"github.com/ba2512005/wire-pod/chipper/pkg/initwirepod"
	stt "github.com/ba2512005/wire-pod/chipper/pkg/wirepod/stt/leopard"
)

func main() {
	initwirepod.StartFromProgramInit(stt.Init, stt.STT, stt.Name)
}
