package sanitizer

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strings"
)

// ProcessChart applies the v9.0.0 Industrial Flow-QA Processor logic.
// Implements Alternation Efficiency metric and automated pattern pruning.
func ProcessChart(chartContent string) string {
	// Extract notes section
	notesRegex := regexp.MustCompile(`(?s)#NOTES:\n(.*?);`)
	notesMatch := notesRegex.FindStringSubmatch(chartContent)
	if len(notesMatch) < 2 {
		return chartContent
	}

	notesData := notesMatch[1]
	measures := strings.Split(notesData, ",")
	var sanitizedMeasures []string

	lastStepCol := -1

	for _, measure := range measures {
		lines := strings.Split(strings.TrimSpace(measure), "\n")
		var sanitizedLines []string
		for _, line := range lines {
			line = strings.TrimSpace(line)
			if line == "" {
				continue
			}

			// 1. No Hands/Quads: Limit to max 2 steps per line
			stepCount := strings.Count(line, "1") + strings.Count(line, "2") + strings.Count(line, "4")
			newLine := []rune(line)

			if stepCount > 2 {
				count := 0
				for i, char := range newLine {
					if char == '1' || char == '2' || char == '4' {
						count++
						if count > 2 {
							newLine[i] = '0'
						}
					}
				}
			}

			// 2. No Double-Steps / Jacks
			var currentStepCols []int
			for i, char := range newLine {
				if char == '1' || char == '2' || char == '4' {
					currentStepCols = append(currentStepCols, i)
				}
			}

			if len(currentStepCols) == 1 {
				if currentStepCols[0] == lastStepCol {
					// Remove jack to enforce alternating flow
					newLine[currentStepCols[0]] = '0'
				} else {
					lastStepCol = currentStepCols[0]
				}
			}

			sanitizedLines = append(sanitizedLines, string(newLine))
		}
		sanitizedMeasures = append(sanitizedMeasures, strings.Join(sanitizedLines, "\n"))
	}

	// Flow QA: Alternation Efficiency
	var allNotes strings.Builder
	for _, m := range sanitizedMeasures {
		allNotes.WriteString(strings.ReplaceAll(m, "\n", ""))
	}

	var steps []int
	for i, c := range allNotes.String() {
		if c == '1' || c == '2' || c == '4' {
			steps = append(steps, i)
		}
	}

	alternations := 0
	for i := 1; i < len(steps); i++ {
		if steps[i]%4 != steps[i-1]%4 {
			alternations++
		}
	}

	efficiency := 100.0
	if len(steps) > 1 {
		efficiency = (float64(alternations) / float64(len(steps)-1)) * 100.0
	}
	fmt.Printf("  [Flow-QA] Alternation Efficiency: %.2f%%\n", efficiency)

	newNotesData := "#NOTES:\n" + strings.Join(sanitizedMeasures, ",\n") + "\n;"
	return notesRegex.ReplaceAllString(chartContent, newNotesData)
}

// SanitizeSSC processes an entire stepmania SSC file
func SanitizeSSC(inputPath, outputPath string) error {
	contentBytes, err := ioutil.ReadFile(inputPath)
	if err != nil {
		return err
	}
	content := string(contentBytes)

	charts := strings.Split(content, "//---------------")
	if len(charts) == 0 {
		return fmt.Errorf("invalid SSC format")
	}

	header := charts[0]
	var processedCharts []string

	for _, chart := range charts[1:] {
		processedCharts = append(processedCharts, ProcessChart(chart))
	}

	var finalContent strings.Builder
	finalContent.WriteString(header)
	for _, chart := range processedCharts {
		finalContent.WriteString("//---------------" + chart)
	}

	return ioutil.WriteFile(outputPath, []byte(finalContent.String()), 0644)
}
