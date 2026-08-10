import {test,expect} from '@playwright/test'

const BASE_URL = process.env.APP_BASE_URL ?? 'https://todo.qacart.com';
const TEST_EMAIL = process.env.APP_TEST_EMAIL ?? 'ayaali20@gmail.com';
const TEST_PASSWORD = process.env.APP_TEST_PASSWORD ?? 'Aya123ali@';
const TEST_FIRST_NAME = process.env.APP_TEST_FIRST_NAME ?? 'Aya';

test("should be able to login using api", async ({request}) =>{

    const apiReq = await request.post(`${BASE_URL}/api/v1/users/login`,
        {data:
            {
                email: TEST_EMAIL,
                password: TEST_PASSWORD
            }
        }
    )

    const body = await apiReq.json();
    console.log(body.firstName)

    //console.log(await apiReq.json());
    await expect(apiReq.ok).toBeTruthy();
    await expect(await apiReq.json()).toHaveProperty("firstName", TEST_FIRST_NAME)
})
