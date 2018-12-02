use log::error;
use std::fmt::Display;

pub trait LoggedResult {
    type Item;
    fn unwrap_or_log(self, default: Self::Item) -> Self::Item;

    fn log_err(self) -> Self;
}

impl<T, E> LoggedResult for Result<T, E>
where
    E: Display,
{
    type Item = T;
    fn unwrap_or_log(self, default: T) -> T {
        self.log_err().unwrap_or(default)
    }

    fn log_err(self) -> Self {
        self.map_err(|e| {
            error!("{}", e);
            e
        })
    }
}
