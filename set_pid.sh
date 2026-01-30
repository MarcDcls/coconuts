# Copyright 2026 Marc Duclusaud

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

#     http://www.apache.org/licenses/LICENSE-2.0

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <id> <kp> <ki>"
    exit 1
fi

uv run software/set_pid.py "$@"
