#include "crow.h"
#include "iostream"
#include "random"
#include "ctime"

class Calculatios {
public:
    int randomNumber(int start, int end)
    {
        std::srand(std::time(0));
        int randomNumber = std::rand() % (end - start + 1) + start;

        return randomNumber;
    }

    std::vector<int> generateNumbers(int num)
    {
        std::vector<int> res;
        for (int i = 1; i < num + 1; i++)
        {
            res.push_back(i);
        }
        return res;
    }

    std::vector<std::vector<int>> caclulateFreeSeats(int rows, int seats_per_row, std::vector<std::vector<int>> booked_seats)
    {
        std::vector<int> rows_total = generateNumbers(rows);
        std::vector<int> seats_per_row_total = generateNumbers(seats_per_row);

        std::vector<std::vector<int>> result;

        for (int row : rows_total)
        {
            for (int seat_in_row : seats_per_row_total)
            {
                std::vector<int> temp = { row, seat_in_row };
                bool flag = false;
                for (std::vector<int> seat : booked_seats)
                {
                    if (temp == seat)
                    {
                        flag = true;
                        break;
                    }
                }
                if (flag)
                {
                    temp.push_back(-2);
                    result.push_back(temp);
                }
                else
                {
                    temp.push_back(-1);
                    result.push_back(temp);
                }

            }
        }
        return result;
    }

};


int main()
{
    crow::SimpleApp app;
    CROW_ROUTE(app, "/")([]() {
        return "Hello world";
        });


    CROW_ROUTE(app, "/post").methods(crow::HTTPMethod::Post)([](const crow::request& req) {
        auto body = crow::json::load(req.body);
        if (!body || !body.has("booked_seats") || !body.has("rows") || !body.has("seats_per_row"))
            return crow::response(400, "Invalid JSON or missing 'name' field");

        std::vector<std::vector<int>> booked_seats;

        for (const auto& seat : body["booked_seats"]) {
            std::vector<int> seat_vector;
            seat_vector.push_back(seat[0].i());
            seat_vector.push_back(seat[1].i());
            booked_seats.push_back(seat_vector);
        }

        int rows = body["rows"].i();
        int seats_per_row = body["seats_per_row"].i();

        Calculatios calucatort =  Calculatios();

        std::vector<std::vector<int>> result = calucatort.caclulateFreeSeats(rows, seats_per_row, booked_seats);


        crow::json::wvalue res_json;
        res_json["message"] = result;


        return crow::response(res_json);
        });

    app.port(8080).multithreaded().run();
}