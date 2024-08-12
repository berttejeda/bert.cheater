package findCMD

import (
	appConfig "github.com/berttejeda/bert.cheater/config"
	"bufio"
	color "github.com/fatih/color"
	"fmt"
	logger "github.com/sirupsen/logrus"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	utils "github.com/berttejeda/bert.cheater/utils"
)

var headersPattern, err = regexp.Compile("^# ")

type linePrintMap struct {
	LowerBoundary int
	UpperBoundary int
}

func readFileIntoMemory(filePath string) []string {

	// Returns file contents as a string array

	var lines []string

	// Open the file
	file, err := os.Open(filePath)
	if err != nil {
		logger.Fatalf("Error opening: %v", err)
	}
	defer file.Close()

	// Read the entire file into memory
	content, err := ioutil.ReadAll(file)
	if err != nil {
		logger.Fatalf("Error reading file into memory: %v", err)
	}

	lines = strings.Split(string(content), "\n")

	// Convert the byte slice to
	// a string and return the result
	return lines
}

// findIndex function returns the index of the target item in the array
func findIntIndex(arr []int, target int) int {
	for i, v := range arr {
		if v == target {
			return i
		}
	}
	return -1 // return -1 if the item is not found
}

func getMatchedHeaderLineNumbers(lines []string, topicsPattern *regexp.Regexp) ([]int, []int, []int, error) {

	// Get Matched Header Line Number

	var allLineNumbers []int
	var allHeaderLineNumbers []int
	var matchedHeaderLineNumbers []int

	for i, line := range lines {
		lineNumber := i + 1
		// Check if the line matches the regular expression
		if topicsPattern.MatchString(line) {
			matchedHeaderLineNumbers = append(matchedHeaderLineNumbers, lineNumber)
		}
		if headersPattern.MatchString(line) {
			allHeaderLineNumbers = append(allHeaderLineNumbers, lineNumber)
		}
		allLineNumbers = append(allLineNumbers, lineNumber)
	}

	return matchedHeaderLineNumbers, allHeaderLineNumbers, allLineNumbers, err
}

func printMatchedLines(cheatFile string, lines []string, matchedHeaderLineNumbers []int, allHeaderLineNumbers []int, allLineNumbers []int, config *appConfig.Config) {

	linePrintMapArraySize := len(matchedHeaderLineNumbers)
	linePrintMapArray := make([]linePrintMap, linePrintMapArraySize)
	var currHeaderLineNumberIndex int
	var nextHeaderLineNumber int

	headerColor := color.New(color.FgMagenta)
	bodyColor := color.New(color.FgGreen)

	if len(matchedHeaderLineNumbers) > 0 {
		logger.Info("Matched against", cheatFile)
	}

	// Build the Map of lines to be printed
	for index, headerLineNumber := range matchedHeaderLineNumbers {
		//nextIndex := index + 1
		currHeaderLineNumberIndex = findIntIndex(allHeaderLineNumbers, headerLineNumber)
		nextHeaderLineNumberIndex := currHeaderLineNumberIndex + 1
		if nextHeaderLineNumberIndex > len(allHeaderLineNumbers)-1 {
			nextHeaderLineNumber = allHeaderLineNumbers[nextHeaderLineNumberIndex-1]
		} else {
			nextHeaderLineNumber = allHeaderLineNumbers[nextHeaderLineNumberIndex]
		}
		lastHeaderLineNumber := allHeaderLineNumbers[len(allHeaderLineNumbers)-1]
		lastMatchedHeaderLineNumber := matchedHeaderLineNumbers[len(matchedHeaderLineNumbers)-1]
		lastLine := allLineNumbers[len(allLineNumbers)-1]
		if headerLineNumber != lastMatchedHeaderLineNumber || headerLineNumber < lastHeaderLineNumber {
			linePrintMapArray[index] = linePrintMap{LowerBoundary: headerLineNumber, UpperBoundary: nextHeaderLineNumber}
		} else {
			linePrintMapArray[index] = linePrintMap{LowerBoundary: headerLineNumber, UpperBoundary: lastLine}
		}
	}

	// Iterate through the file lines, printing only
	// the lines that satisfy the linePrintMapArray
	for i, line := range lines {
		lineNumber := i + 1
		isMatch := utils.IntArrayContains(matchedHeaderLineNumbers, lineNumber)
		isHeader := headersPattern.MatchString(line)
		for _, linePrintMap := range linePrintMapArray {
			if isMatch && isHeader && lineNumber >= linePrintMap.LowerBoundary && lineNumber < linePrintMap.UpperBoundary {
				headerColor.Println(line)
			} else if !isHeader && lineNumber >= linePrintMap.LowerBoundary && lineNumber < linePrintMap.UpperBoundary {
				bodyColor.Println(line)
			}
			if lineNumber == linePrintMap.UpperBoundary && lineNumber != 1 {
				if !config.NoPauseBetweenTopics {
					fmt.Println("ENTER => CONTINUE TO NEXT TOPIC or 'q' to quit")
					reader := bufio.NewReader(os.Stdin)
					userInput, err := reader.ReadString('\n')
					if err != nil {
						fmt.Println("Error reading input:", err)
						return
					}

					// Remove the newline character from the input
					userInput = userInput[:len(userInput)-1]
					if userInput == "q" {
						os.Exit(0)
					}
				}
			}
		}

	}

}

// Cheat file processor
func ProcessCheatFiles(config *appConfig.Config) {

	fileExtensions := config.FileExtensions

	searchPaths := config.SearchPaths

	// Compile the regular expressions

	topicStrings := config.Topics
	var topicPermutationsMatrix [][]string
	var topicPermutations []string
	utils.ArrayPermute(topicStrings, 0, len(topicStrings)-1, &topicPermutationsMatrix)
	for i := range topicPermutationsMatrix {
		p := strings.Join(topicPermutationsMatrix[i], ".*")
		topicPermutations = append(topicPermutations, p+".*")
	}

	topicsRegex := fmt.Sprintf("^#.*%s", strings.Join(topicPermutations, "|^#.*"))
	topicsPattern, err := regexp.Compile(topicsRegex)

	logger.Debug("Topics Permutations ", topicPermutations)
	logger.Debug("Topics Pattern is ", topicsPattern)

	if err != nil {
		logger.Fatalf("Error compiling regex: %v", err)
	}

	// Ensure array of file extensions matches format of .{{ extension }}
	for i := range fileExtensions {
		(fileExtensions)[i] = fmt.Sprintf(".%s", (fileExtensions)[i])
	}

	for _, rootDir := range searchPaths {

		logger.Debug(fmt.Sprintf("Searching %s for cheat files", rootDir))

		err := filepath.WalkDir(rootDir, func(path string, d os.DirEntry, err error) error {
			if err != nil {
				return err
			}

			isMatch := utils.StringArrayContains(fileExtensions, filepath.Ext(path))

			var matchedHeaderLineNumbers []int
			var allHeaderLineNumbers []int
			var allLineNumbers []int

			if !d.IsDir() && isMatch {

				logger.Debug(fmt.Sprintf("Found %s", path))
				lines := readFileIntoMemory(path)
				matchedHeaderLineNumbers, allHeaderLineNumbers, allLineNumbers, _ = getMatchedHeaderLineNumbers(lines, topicsPattern)
				printMatchedLines(path, lines, matchedHeaderLineNumbers, allHeaderLineNumbers, allLineNumbers, config)

			}

			return nil
		})

		if err != nil {
			logger.Error(fmt.Sprintf("Error walking the path %q: %v\n", rootDir, err))
		}

	}

	return
}
