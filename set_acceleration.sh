# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <acceleration_value> <motor_ids>"
    exit 1
fi

uv run software/set_acceleration.py "$@"