use std::collections::VecDeque;
use std::time::Duration;

const WINDOW_SIZE: usize = 100;

#[derive(Clone)]
pub struct DurationAggregator {
    window: VecDeque<Duration>,
    window_size: usize,
    sum: Duration,
    min: Option<Duration>,
    max: Option<Duration>,
}

impl DurationAggregator {
    pub fn init() -> DurationAggregator {
        DurationAggregator::with_window(WINDOW_SIZE)
    }

    pub fn with_window(window_size: usize) -> DurationAggregator {
        DurationAggregator {
            min: None,
            max: None,
            window_size,
            window: VecDeque::with_capacity(window_size + 1),
            sum: Duration::default(),
        }
    }

    pub fn ingest(&mut self, value: Duration) {
        self.min = Some(self.min.unwrap_or(value).min(value));
        self.max = Some(self.max.unwrap_or(value).max(value));
        self.window.push_front(value);

        self.sum += value;
        if self.window.len() > self.window_size {
            let popped = self.window.pop_back().unwrap();
            self.sum -= popped;

            if Some(popped) == self.min {
                self.min = self.window.iter().cloned().min();
            }
            if Some(popped) == self.max {
                self.max = self.window.iter().cloned().max();
            }
        }
    }

    pub fn average(&self) -> Duration {
        if self.window.is_empty() {
            Duration::default()
        } else {
            self.sum / (self.window.len() as u32)
        }
    }

    pub fn average_secs(&self) -> f64 {
        let duration = self.average();
        duration.as_secs_float()
    }

    pub fn min_secs(&self) -> Option<f64> {
        self.min.map(|d| d.as_secs_float())
    }

    pub fn max_secs(&self) -> Option<f64> {
        self.max.map(|d| d.as_secs_float())
    }
}

pub struct CountHistorgram {
    bins: VecDeque<u64>,
    max_num_bins: usize,
}

trait AsSecsFloat {
    fn as_secs_float(&self) -> f64;
}

impl AsSecsFloat for Duration {
    fn as_secs_float(&self) -> f64 {
        (self.as_secs() as f64) + (f64::from(self.subsec_micros()) / 1_000_000.0)
    }
}

impl CountHistorgram {
    pub fn init(max_num_bins: usize) -> CountHistorgram {
        assert!(max_num_bins != 0);
        let mut bins = VecDeque::with_capacity(max_num_bins);
        bins.push_front(0);
        CountHistorgram { max_num_bins, bins }
    }

    pub fn rollover(&mut self) {
        self.bins.push_front(0);
        if self.bins.len() > self.max_num_bins {
            self.bins.pop_back();
        }
    }

    pub fn is_empty(&self) -> bool {
        !self.bins.iter().any(|count| *count > 0)
    }

    pub fn inc(&mut self) {
        self.bins[0] += 1;
    }

    pub fn get_current(&self) -> u64 {
        self.bins[0]
    }

    pub fn get_total(&self) -> u64 {
        self.bins.iter().sum()
    }
}

#[cfg(test)]
fn build_durations(secs: &[u64]) -> DurationAggregator {
    let mut returned = DurationAggregator::with_window(5);

    for duration in secs {
        returned.ingest(Duration::new(*duration, 0));
    }
    returned
}

#[test]
fn test_min_max() {
    let durations = build_durations(&[1, 2, 3, 4]);
    assert!((durations.max_secs().unwrap() - 4.).abs() < f64::EPSILON);
    assert!((durations.min_secs().unwrap() - 1.).abs() < f64::EPSILON);
}

#[test]

fn test_min_max_rollover1() {
    let durations = build_durations(&[1, 5, 3, 4, 3, 2, 3]);

    assert!((durations.max_secs().unwrap() - 4.).abs() < f64::EPSILON);
    assert!((durations.min_secs().unwrap() - 2.).abs() < f64::EPSILON);
}

#[test]
fn test_min_max_rollover2() {
    let durations = build_durations(&[1, 5, 1, 5, 3, 2, 3]);

    assert!((durations.max_secs().unwrap() - 5.).abs() < f64::EPSILON);
    assert!((durations.min_secs().unwrap() - 1.).abs() < f64::EPSILON);
}

#[test]
fn test_no_items() {
    let durations = build_durations(&[]);
    assert!(durations.max_secs().is_none());
    assert!(durations.min_secs().is_none());
}
