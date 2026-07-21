package sanitizer

import (
	"testing"
	"strings"
)

func TestProcessChart(t *testing.T) {
	testChart := `#NOTES:
0000
1001
1111
;`

	sanitized := ProcessChart(testChart)

	if strings.Contains(sanitized, "1111") {
		t.Errorf("Expected quads to be pruned. Got: %s", sanitized)
	}

	if !strings.Contains(sanitized, "1001") {
		t.Errorf("Expected valid step to remain. Got: %s", sanitized)
	}
}
