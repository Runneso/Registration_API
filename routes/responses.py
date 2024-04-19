from schemas import (GetUser,
                     Token, )

from dataclasses import dataclass
from typing import List

from fastapi import status


@dataclass
class UsersResponses:
    get_users: dict
    create_user: dict
    sign_in: dict
    my_profile: dict
    update_profile: dict
    update_password: dict
    my_friends: dict
    add_friend: dict
    remove_friend: dict


@dataclass
class Responses:
    users: UsersResponses


def load_responses() -> Responses:
    return Responses(
        users=UsersResponses(
            get_users={
                status.HTTP_200_OK: {
                    "content": {
                        "application/json": {
                            "example": [
                                {
                                    "id": 0,
                                    "username": "Alex",
                                    "email": "alex@gmail.com",
                                    "createdAt": "2024-04-17T13:07:25.709Z"
                                }
                            ]
                        }
                    },
                    "model": List[GetUser],
                },
            },
            create_user={
                status.HTTP_201_CREATED: {
                    "content": {
                        "application/json": {
                            "example": {
                                "access_token": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                                "token_type": "bearer"
                            }
                        }
                    },
                    "model": Token,
                },
                status.HTTP_409_CONFLICT: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Conflict user data!"}
                        }
                    },
                    "description": "Conflict Error",
                },
                status.HTTP_429_TOO_MANY_REQUESTS: {
                    "content": {
                        "application/json": {
                            "example": {"error": "Rate limit exceeded: Too many requests, please try later!"}
                        }
                    },
                    "description": "Rate limit Error",
                }
            },
            sign_in={
                status.HTTP_200_OK: {
                    "content": {
                        "application/json": {
                            "example": {
                                "access_token": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                                "token_type": "bearer"
                            }
                        }
                    },
                    "model": Token,
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Invalid password!"}
                        }
                    },
                    "description": "Unauthorized Error",
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "User doesnt exist!"}
                        }
                    },
                    "description": "Not found Error",
                },
                status.HTTP_429_TOO_MANY_REQUESTS: {
                    "content": {
                        "application/json": {
                            "example": {"error": "Rate limit exceeded: Too many requests, please try later!"}
                        }
                    },
                    "description": "Rate limit Error",
                }
            },
            my_profile={
                status.HTTP_200_OK: {
                    "content": {
                        "application/json": {
                            "example": {
                                "id": 0,
                                "username": "Alex",
                                "email": "alex@gmail.com",
                                "createdAt": "2024-04-17T13:07:25.709Z"
                            }
                        }
                    },
                    "model": GetUser,
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Invalid JWT token!"}
                        }
                    },
                    "description": "Unauthorized Error",
                }
            },
            update_profile={
                status.HTTP_201_CREATED: {
                    "content": {
                        "application/json": {
                            "example": {
                                "id": 0,
                                "username": "Alex",
                                "email": "alex@gmail.com",
                                "createdAt": "2024-04-17T13:07:25.709Z"
                            }
                        }
                    },
                    "model": GetUser,
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Invalid JWT token!"}
                        }
                    },
                    "description": "Unauthorized Error",
                }
            },
            update_password={
                status.HTTP_201_CREATED: {
                    "content": None,
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Invalid JWT token!"}
                        }
                    },
                    "description": "Unauthorized Error",
                },
            },
            my_friends={
                status.HTTP_200_OK: {
                    "content": {
                        "application/json": {
                            "example": {
                                1,
                            }
                        }
                    },
                    "model": List[int],
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Invalid JWT token!"}
                        }
                    },
                    "description": "Unauthorized Error",
                }
            },
            add_friend={
                status.HTTP_201_CREATED: {
                    "content": {
                        "application/json": {
                            "example": {
                                1, 2
                            }
                        }
                    },
                    "model": List[int],
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Invalid JWT token!"}
                        }
                    },
                    "description": "Unauthorized Error",
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Friend not found!"}
                        }
                    },
                    "description": "Not found Error",
                },
                status.HTTP_409_CONFLICT: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Friend already in user`s friends!"}
                        }
                    },
                    "description": "Conflict Error",
                }
            },
            remove_friend={
                status.HTTP_204_NO_CONTENT: {
                    "content": None,
                },
                status.HTTP_401_UNAUTHORIZED: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Invalid JWT token!"}
                        }
                    },
                    "description": "Unauthorized Error",
                },
                status.HTTP_404_NOT_FOUND: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "Friend not found!"}
                        }
                    },
                    "description": "Not found Error",
                },
                status.HTTP_409_CONFLICT: {
                    "content": {
                        "application/json": {
                            "example": {"detail": "No same user in user`s friends!"}
                        }
                    },
                    "description": "Conflict Error",
                }
            }
        )
    )
