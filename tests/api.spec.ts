import {test,expect} from '@playwright/test'

// Validates that the login API returns the expected user information upon success.
test("should be able to login using api", async ({request}) =>{

    const apiReq = await request.post("https://todo.qacart.com/api/v1/users/login",
        {data:
            {
                email: "ayaali20@gmail.com",
                password: "Aya123ali@"
            }
        }
    )

    const body = await apiReq.json();
    console.log(body.firstName)

    // Confirm the request succeeded and the response includes the expected firstName property.
    await expect(apiReq.ok).toBeTruthy();
    await expect(await apiReq.json()).toHaveProperty("firstName","Aya")
})
