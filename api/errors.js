/* Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ----------------------------------------------------------------------------
 */
'use strict'

class BadRequest extends Error {
  constructor (message) {
    super(message)
    this.status = 400
  }
}

class Unauthorized extends Error {
  constructor (message) {
    super(message)
    this.status = 401
  }
}

class NotFound extends Error {
  constructor (message) {
    super(message)
    this.status = 404
  }
}

class InternalServerError extends Error {
  constructor (message) {
    super(message)
    this.status = 500
  }
}

module.exports = {
  BadRequest,
  Unauthorized,
  NotFound,
  InternalServerError
}
