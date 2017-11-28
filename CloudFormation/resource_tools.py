"""
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from botocore.vendored import requests
import boto3
import json
import string
import random
import re
import time


def send(event, context, responseStatus, responseData, physicalResourceId):
    responseUrl = event['ResponseURL']

    responseBody = {
        'Status': responseStatus,
        'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
        'PhysicalResourceId': physicalResourceId or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

    return


def stack_name(event):
    try:
        response = event['ResourceProperties']['StackName']
    except Exception:
        response = None
    return response


def wait_for_channel_states(medialive, channel_id, states):
    current_state = ''
    while current_state not in states:
        time.sleep(5)
        current_state = medialive.describe_channel(
            ChannelId=channel_id)['State']
    return current_state


def wait_for_input_states(medialive, input_id, states):
    current_state = ''
    while current_state not in states:
        time.sleep(5)
        current_state = medialive.describe_input(InputId=input_id)['State']
    return current_state
