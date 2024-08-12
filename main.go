package main

import (
		"fmt"
    "os"
    config "github.com/berttejeda/bt-cheater/config"
    findCMD "github.com/berttejeda/bt-cheater/commands/find"
    "github.com/alecthomas/kingpin/v2"
    logger "github.com/sirupsen/logrus"
)

var (
  app         = kingpin.New("bt-cheater", "Search through your markdown notes by keyword")
  verbose     = app.Flag("verbose", "Enable verbose mode").Short('v').Bool()
  debug       = app.Flag("debug", "Enable debug mode").Short('d').Bool()
  jsonLogging = app.Flag("json-logging", "Enable json log format").Short('J').Bool()
  find        = app.Command("find", "Retrieve cheat notes and display in terminal")
  any         = find.Flag("any", "Match 'any' topic as opposed to 'all'").Short('a').Bool()
  nopause     = find.Flag("no-pause", "Don't pause between matched topics").Short('n').Bool()
  filters     = find.Flag("filters", "File extensions to math when searching").Short('f').Default("md", "txt").Strings()
  paths       = find.Flag("paths", "File search paths").Short('p').Default(".").Strings()
  topics      = find.Arg("args", "Topics to match").Strings()
)

func main() {

	app.UsageTemplate(kingpin.DefaultUsageTemplate).Version("0.1.0").Author("Bert Tejeda")

	cli := kingpin.MustParse(app.Parse(os.Args[1:]))

	// Enable Debug Logging if applicable
	if *debug {
		logger.SetLevel(logger.DebugLevel)
	}

	options, err := config.InitOptions()

	if err != nil {
	    logger.Error(err)
	} 		

	// Enable JSON Logging if applicable
	if *jsonLogging {
		logger.SetFormatter(&logger.JSONFormatter{})
	}

  switch cli {

  // Find cheat notes
  case find.FullCommand():

		if *filters == nil {
			fmt.Println("nil!")
		}

		var MatchAny bool = false
		var NoPauseBetweenTopics bool = false

		if *any {
			MatchAny = true
		} else if options.MatchAny {
			MatchAny = true
		}

		if *nopause {
			NoPauseBetweenTopics = true
		} else if options.NoPauseBetweenTopics {
			NoPauseBetweenTopics = true
		}		

  	appConfig := config.InitConfig(*topics).WithFileExtensions(*filters).WithSearchPaths(options.Search.Paths, *paths).WithNoPause(NoPauseBetweenTopics).WithMatchAny(MatchAny)

    findCMD.ProcessCheatFiles(appConfig)

	}

}