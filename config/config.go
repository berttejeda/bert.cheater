package options

import (
  "fmt"
	logger "github.com/sirupsen/logrus"
  "github.com/spf13/viper"
  utils "github.com/berttejeda/bert.cheater/utils"
)

type Search struct {
 Paths []string `mapstructure:"paths"`
 Filters []string `mapstructure:"filters"`
}

type Options struct {
 Search Search  `mapstructure:"search"`
 NoPauseBetweenTopics bool `mapstructure:"pause"`
 MatchAny bool `mapstructure:"any"`
 ConfigFileUsed string
}

func InitOptions(configFile string) (Options, error) {

	if len(configFile) > 0 {
		viper.SetConfigFile(configFile)
	} else {
		viper.SetConfigName("config") // options file name without extension
		viper.SetConfigType("yaml")
		viper.AddConfigPath("./")
		configUserPath, _ := utils.FSOExpandUser("~/.bert.cheater")
		viper.AddConfigPath(configUserPath) // options file path
		viper.AddConfigPath("/etc/bert.cheater")
		viper.AutomaticEnv()             // read value ENV variable
	}

	err := viper.ReadInConfig()

	logger.Debug("Using options file: ", viper.ConfigFileUsed())

	if err != nil {
	  logger.Warning("Failed to parse options file,error was ", err, " Using defaults")
	}

	var options Options

	if err := viper.Unmarshal(&options); err != nil {
		fmt.Println(err)
		return options, err
	}

	options.ConfigFileUsed = viper.ConfigFileUsed()

	return options, err

}

type Config struct {
    // Required
    Topics []string
    SearchPaths  []string
    FileExtensions []string
    // Optional
    NoPauseBetweenTopics bool
    MatchAny bool
}

// Each optional attribute will have its own public method
func (c *Config) WithNoPause(NoPauseBetweenTopics bool) *Config {
    c.NoPauseBetweenTopics = NoPauseBetweenTopics
    return c
}

func (c *Config) WithMatchAny(MatchAny bool) *Config {
    c.MatchAny = MatchAny
    return c
}


func (c *Config) WithFileExtensions(r []string) *Config {
    c.FileExtensions = r
    return c
}

func (c *Config) WithSearchPaths(default_paths []string, paths []string) *Config {
    
    var searchPaths []string

    if len(default_paths) > 0 {
      searchPaths = default_paths
    } else {
      searchPaths = paths
    }

    for i := range searchPaths {
        (searchPaths)[i], _ = utils.FSOExpandUser((searchPaths)[i])
    }

    c.SearchPaths = searchPaths
    return c
}

// This only accepts the required options as params
func InitConfig(topics []string) *Config {
    // First fill in the options with default values
    return &Config{
    	Topics: topics,
    	SearchPaths: []string{"."},
    	FileExtensions: []string{".*"},
    	NoPauseBetweenTopics: false, 
    	MatchAny: false,
    }
}