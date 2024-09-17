# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional
import requests
import json

from langchain.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional


class BaseLLM(LLM):
    
    temperature: Optional[float] = 0.5
    url: Any = ""
    headers : Optional[Any]  = {}
    body : Optional[Any]  = {}
    

    def _call(
        self,
        prompt: Optional[str]="",
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        
        if prompt != "":
            self.body["prompt"] = prompt
        r = requests.post(self.url,  json=self.body,headers=self.headers)
        try:
            model_out = json.loads(r.content)
        except Exception as e:
            model_out = {}
            
        
        return model_out

   
        
    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        
        return "hi"
        
    @property
    def _llm_type(self) -> str:
        return "rest llm"
    
    @property
    def _identifying_params(self) -> dict:
        return {
            "url": self.url,
        }
    
    