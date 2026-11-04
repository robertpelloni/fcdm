package hardware

import (
	"reflect"
	"testing"
)

func TestParseTelemetryLine(t *testing.T) {
	tests := []struct {
		name      string
		line      string
		want      []int
		expectErr bool
	}{
		{
			name:      "Valid 9-panel line",
			line:      "0,0,1024,0,50,0,0,0,4000\n",
			want:      []int{0, 0, 1024, 0, 50, 0, 0, 0, 4000},
			expectErr: false,
		},
		{
			name:      "Valid 9-panel with whitespaces",
			line:      "  10, 20, 30, 40, 50, 60, 70, 80, 90  ",
			want:      []int{10, 20, 30, 40, 50, 60, 70, 80, 90},
			expectErr: false,
		},
		{
			name:      "Too few panels",
			line:      "100,200,300,400",
			want:      nil,
			expectErr: true,
		},
		{
			name:      "Too many panels",
			line:      "1,2,3,4,5,6,7,8,9,10",
			want:      nil,
			expectErr: true,
		},
		{
			name:      "Invalid integer",
			line:      "0,0,1024,foo,50,0,0,0,4000",
			want:      nil,
			expectErr: true,
		},
		{
			name:      "Empty line",
			line:      "",
			want:      nil,
			expectErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := ParseTelemetryLine(tt.line)
			if (err != nil) != tt.expectErr {
				t.Fatalf("ParseTelemetryLine() error = %v, expectErr %v", err, tt.expectErr)
			}
			if !tt.expectErr && !reflect.DeepEqual(got, tt.want) {
				t.Errorf("ParseTelemetryLine() got = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestGetTelemetryConcurrency(t *testing.T) {
	// Verify that reading telemetry while simulated telemetry updates does not race or panic
	for i := 0; i < 50; i++ {
		tel := GetTelemetry(true)
		if len(tel) != 9 {
			t.Errorf("expected 9 telemetry values, got %d", len(tel))
		}
	}
}
