package ai.d5data.exam;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class ApiIntegrationTest {
    @Autowired MockMvc mvc;

    @Test
    void helloRequiresAuthentication() throws Exception {
        mvc.perform(get("/api/hello")).andExpect(status().isUnauthorized());
    }

    @Test
    void loginCreatesSessionThatCanCallHello() throws Exception {
        MockHttpSession session = (MockHttpSession) mvc.perform(post("/api/login")
                .contentType("application/json")
                .content("{\"username\":\"test\",\"password\":\"123456\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.message").value("login_success"))
            .andReturn().getRequest().getSession(false);

        mvc.perform(get("/api/hello").session(session))
            .andExpect(status().isOk())
            .andExpect(content().string("Hello World"));
    }
}
